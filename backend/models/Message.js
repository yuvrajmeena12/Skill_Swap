const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema(
  {
    sender: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    recipient: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    swapRequest: { type: mongoose.Schema.Types.ObjectId, ref: 'SwapRequest', default: undefined },
    skill: { type: mongoose.Schema.Types.ObjectId, ref: 'Skill', default: undefined },
    text: { type: String, required: true, trim: true },
    read: { type: Boolean, default: false },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Message', messageSchema);
