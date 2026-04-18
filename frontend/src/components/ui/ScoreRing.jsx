// src/components/ui/ScoreRing.jsx
import PropTypes from "prop-types";

const ScoreRing = ({ pct = 0, size = 80 }) => {
  const R    = size * 0.39;
  const C    = 2 * Math.PI * R;
  const dash = (pct / 100) * C;
  const cx   = size / 2;

  const strokeColor =
    pct >= 70 ? "#10B981" : pct >= 40 ? "#FBBF24" : "#EF4444";

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      className="flex-shrink-0"
    >
      {/* Track */}
      <circle
        cx={cx} cy={cx} r={R}
        fill="none"
        stroke="#2a2a3e"
        strokeWidth={size * 0.07}
      />
      {/* Fill */}
      <circle
        cx={cx} cy={cx} r={R}
        fill="none"
        stroke={strokeColor}
        strokeWidth={size * 0.07}
        strokeDasharray={`${dash} ${C}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`}
        style={{ transition: "stroke-dasharray 0.5s ease" }}
      />
      {/* Label */}
      <text
        x={cx} y={cx + 5}
        textAnchor="middle"
        fill="#e8e8f0"
        fontSize={size * 0.19}
        fontFamily="'Syne', sans-serif"
        fontWeight="700"
      >
        {pct}%
      </text>
    </svg>
  );
};

ScoreRing.propTypes = {
  pct:  PropTypes.number,
  size: PropTypes.number,
};

export default ScoreRing;