import PropTypes from "prop-types";

const Badge = ({ children, variant = "default", className = "" }) => {
  const variants = {
    default: "bg-[#1e1e2e] border border-[#2a2a3e] text-[#a5a5c0]",
    accent:  "bg-violet-600/20 border border-violet-500/40 text-violet-300",
    teal:    "bg-teal-500/20 border border-teal-500/40 text-teal-300",
    easy:    "bg-emerald-500/15 border border-emerald-500/30 text-emerald-400",
    medium:  "bg-yellow-500/15 border border-yellow-500/30 text-yellow-400",
    hard:    "bg-red-500/15 border border-red-500/30 text-red-400",
  };
  return (
    <span
      className={`inline-block px-2.5 py-0.5 rounded-full text-[0.62rem] tracking-widest
        font-mono uppercase ${variants[variant] ?? variants.default} ${className}`}
    >
      {children}
    </span>
  );
};

Badge.propTypes = {
  children:  PropTypes.node.isRequired,
  variant:   PropTypes.oneOf(["default", "accent", "teal", "easy", "medium", "hard"]),
  className: PropTypes.string,
};

export default Badge;