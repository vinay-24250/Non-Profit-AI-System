// src/components/ui/Spinner.jsx
import PropTypes from "prop-types";

const Spinner = ({ size = "sm", light = true }) => {
  const dim = size === "sm" ? "w-3.5 h-3.5" : "w-5 h-5";
  const border = light
    ? "border-white/30 border-t-white"
    : "border-slate-300/30 border-t-slate-600";
  return (
    <span
      className={`inline-block ${dim} rounded-full border-2 ${border} animate-spin`}
    />
  );
};

Spinner.propTypes = {
  size:  PropTypes.oneOf(["sm", "md"]),
  light: PropTypes.bool,
};

export default Spinner;