const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true, trim: true },
    password: { type: String, required: true, minlength: 6 },
    phone: { type: String, default: '' },
    bio: { type: String, default: '' },
    about: { type: String, default: '' },
    qualification: { type: String, default: '' },
    hobbies: { type: String, default: '' },
    awards: { type: String, default: '' },
    location: { type: String, default: '' },
    profilePicUrl: { type: String, default: '' },
    linkedinUrl: { type: String, default: '' },
    instagramUrl: { type: String, default: '' },
    websiteUrl: { type: String, default: '' },
    
    // SkillSwap Verified Badge: Earned strictly through completed and rated interactions (threshold >= 5)
    isVerified: { type: Boolean, default: false },
    trustScore: { type: Number, default: 0 },
    rating: { type: Number, default: 0 },
    ratingCount: { type: Number, default: 0 },
    completedSwapsCount: { type: Number, default: 0 },
    
    // Account verification via OTP
    isEmailVerified: { type: Boolean, default: false },
    otp: { type: String, default: undefined },
    otpExpire: { type: Date, default: undefined },
    otpAttempts: { type: Number, default: 0 },
    otpCooldown: { type: Date, default: undefined },

    role: { type: String, enum: ['user', 'admin'], default: 'user' },
    isBanned: { type: Boolean, default: false },

    // Password reset tokens
    resetPasswordToken: { type: String, default: undefined },
    resetPasswordExpire: { type: Date, default: undefined },
  },
  { timestamps: true }
);

userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

userSchema.methods.matchPassword = async function (entered) {
  return bcrypt.compare(entered, this.password);
};

module.exports = mongoose.model('User', userSchema);
