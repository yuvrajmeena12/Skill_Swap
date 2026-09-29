const mongoose = require('mongoose');

const skillSchema = new mongoose.Schema(
  {
    user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    title: { type: String, required: true, trim: true },
    category: {
      type: String,
      enum: ['Tech', 'Music', 'Language', 'Fitness', 'Art', 'Cooking', 'Academic', 'Other'],
      default: 'Other',
    },
    description: { type: String, default: '' },
    level: { type: String, enum: ['Beginner', 'Intermediate', 'Expert'], default: 'Beginner' },
    type: { type: String, enum: ['teach', 'want'], required: true },
    mode: { type: String, enum: ['online', 'in-person', 'both'], default: 'both' },
    
    // Proof / Certificate for individual skill (supporting documentation).
    // Stored as base64 data URI in MongoDB to maintain persistence.
    // Note: Certificate upload does NOT grant the SkillSwap Verified Badge to the user.
    certificateFile: { type: String, default: '' }, // base64 data URI
    certificateFileName: { type: String, default: '' },
    certificateFileType: { type: String, default: '' },
    hasProof: { type: Boolean, default: false },
    isVerified: { type: Boolean, default: false }, // retained for certificate proof attachment status
  },
  { timestamps: true }
);

module.exports = mongoose.model('Skill', skillSchema);
