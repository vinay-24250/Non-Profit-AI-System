// src/components/ui/Toast.jsx
import { useEffect, useState } from "react";
import PropTypes from "prop-types";

const Toast = ({ message, onDone, duration = 2200 }) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(false);
      setTimeout(onDone, 300);
    }, duration);
    return () => clearTimeout(t);
  }, [duration, onDone]);

  return (
    <div
      className={`fixed bottom-6 right-6 z-50 flex items-center gap-2 px-5 py-3
        rounded-xl bg-teal-400 text-[#0a0a0f] text-sm font-mono font-medium
        shadow-2xl transition-all duration-300
        ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"}`}
    >
      <span>✓</span>
      {message}
    </div>
  );
};

Toast.propTypes = {
  message:  PropTypes.string.isRequired,
  onDone:   PropTypes.func.isRequired,
  duration: PropTypes.number,
};

export default Toast;