const Skill = require('../models/Skill');

// POST /api/skills
const addSkill = async (req, res) => {
  try {
    const { title, category, description, level, type, mode } = req.body;
    if (!title || !type) return res.status(400).json({ message: 'Title and type are required' });

    const skill = await Skill.create({
      user: req.user._id,
      title: title.trim(),
      category: category || 'Other',
      description: description || '',
      level: level || 'Beginner',
      type, // 'teach' or 'want'
      mode: mode || 'both',
    });
    res.status(201).json(skill);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// POST /api/skills/:id/certificate (multipart/form-data, field "certificate")
const uploadCertificate = async (req, res) => {
  try {
    const skill = await Skill.findOne({ _id: req.params.id, user: req.user._id });
    if (!skill) return res.status(404).json({ message: 'Skill not found' });
    if (skill.type !== 'teach') {
      return res.status(400).json({ message: 'Certificates/proof can only be attached to skills you teach' });
    }
    if (!req.file) return res.status(400).json({ message: 'No file uploaded' });

    const base64 = req.file.buffer.toString('base64');
    skill.certificateFile = `data:${req.file.mimetype};base64,${base64}`;
    skill.certificateFileName = req.file.originalname;
    skill.certificateFileType = req.file.mimetype;
    skill.hasProof = true;
    skill.isVerified = true; // Skill proof attached flag
    await skill.save();

    res.json(skill);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// DELETE /api/skills/:id/certificate
const removeCertificate = async (req, res) => {
  try {
    const skill = await Skill.findOne({ _id: req.params.id, user: req.user._id });
    if (!skill) return res.status(404).json({ message: 'Skill not found' });
    skill.certificateFile = '';
    skill.certificateFileName = '';
    skill.certificateFileType = '';
    skill.hasProof = false;
    skill.isVerified = false;
    await skill.save();
    res.json(skill);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/skills
const browseSkills = async (req, res) => {
  try {
    const { category, mode, type, search, excludeSelf } = req.query;
    const query = {};
    if (category) query.category = category;
    if (mode) query.mode = mode;
    if (type && type !== 'all') query.type = type;
    if (search) {
      query.$or = [
        { title: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } },
        { category: { $regex: search, $options: 'i' } },
      ];
    }
    if (excludeSelf !== 'false' && req.user) query.user = { $ne: req.user._id };

    const skills = await Skill.find(query)
      .select('-certificateFile')
      .populate('user', 'name profilePicUrl isVerified trustScore rating ratingCount location completedSwapsCount qualification')
      .sort({ createdAt: -1 });

    res.json(skills);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/skills/:id/certificate
const getCertificate = async (req, res) => {
  try {
    const skill = await Skill.findById(req.params.id).select(
      'certificateFile certificateFileName certificateFileType title'
    );
    if (!skill || !skill.certificateFile) {
      return res.status(404).json({ message: 'No certificate/proof attached for this skill' });
    }
    res.json({
      certificateFile: skill.certificateFile,
      certificateFileName: skill.certificateFileName,
      certificateFileType: skill.certificateFileType,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/skills/mine
const getMySkills = async (req, res) => {
  try {
    const skills = await Skill.find({ user: req.user._id }).select('-certificateFile').sort({ createdAt: -1 });
    res.json(skills);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/skills/user/:userId
const getSkillsByUser = async (req, res) => {
  try {
    const skills = await Skill.find({ user: req.params.userId }).select('-certificateFile').sort({ createdAt: -1 });
    res.json(skills);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// PUT /api/skills/:id
const updateSkill = async (req, res) => {
  try {
    const skill = await Skill.findOne({ _id: req.params.id, user: req.user._id });
    if (!skill) return res.status(404).json({ message: 'Skill not found' });
    Object.assign(skill, req.body);
    await skill.save();
    res.json(skill);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// DELETE /api/skills/:id
const deleteSkill = async (req, res) => {
  try {
    const skill = await Skill.findOneAndDelete({ _id: req.params.id, user: req.user._id });
    if (!skill) return res.status(404).json({ message: 'Skill not found' });
    res.json({ message: 'Skill deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/skills/matches (Smart Match)
const getMatches = async (req, res) => {
  try {
    const myWantSkills = await Skill.find({ user: req.user._id, type: 'want' });
    const myTeachSkills = await Skill.find({ user: req.user._id, type: 'teach' });

    const wantTitles = myWantSkills.map((s) => s.title.toLowerCase().trim()).filter(Boolean);
    const teachTitles = myTeachSkills.map((s) => s.title.toLowerCase().trim()).filter(Boolean);

    if (wantTitles.length === 0 && teachTitles.length === 0) {
      return res.json([]);
    }

    let candidateTeachSkills = [];
    if (wantTitles.length > 0) {
      candidateTeachSkills = await Skill.find({
        type: 'teach',
        user: { $ne: req.user._id },
        title: { $regex: wantTitles.join('|'), $options: 'i' },
      }).populate('user', 'name profilePicUrl isVerified trustScore rating completedSwapsCount location qualification');
    }

    const matchesByUser = {};
    for (const skill of candidateTeachSkills) {
      if (!skill.user) continue;
      const uid = skill.user._id.toString();
      if (!matchesByUser[uid]) {
        matchesByUser[uid] = {
          user: skill.user,
          theyTeach: [],
          theyTeachSkills: [],
          mutualMatch: false,
          iTeachThem: [],
        };
      }
      matchesByUser[uid].theyTeach.push(skill.title);
      matchesByUser[uid].theyTeachSkills.push({
        _id: skill._id,
        title: skill.title,
        category: skill.category,
        level: skill.level,
        hasProof: skill.hasProof || skill.isVerified,
        isVerified: skill.isVerified,
      });
    }

    // Check mutual match
    for (const uid of Object.keys(matchesByUser)) {
      const theirWantSkills = await Skill.find({ user: uid, type: 'want' });
      const theirWantTitles = theirWantSkills.map((s) => s.title.toLowerCase().trim());
      const overlap = teachTitles.filter((t) => theirWantTitles.some((wt) => wt.includes(t) || t.includes(wt)));
      if (overlap.length > 0) {
        matchesByUser[uid].mutualMatch = true;
        matchesByUser[uid].iTeachThem = overlap;
      }
    }

    res.json(Object.values(matchesByUser));
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  addSkill,
  browseSkills,
  getMySkills,
  updateSkill,
  deleteSkill,
  getMatches,
  getSkillsByUser,
  uploadCertificate,
  removeCertificate,
  getCertificate,
};
