// src/components/triage/EntityCard.jsx
import PropTypes from "prop-types";

const ENTITY_LABELS = {
  persons:       { label: "Persons",       color: "text-violet-400 border-violet-500/30 bg-violet-500/10"   },
  organizations: { label: "Organizations", color: "text-teal-400   border-teal-500/30   bg-teal-500/10"     },
  dates:         { label: "Dates",         color: "text-yellow-400 border-yellow-500/30 bg-yellow-500/10"   },
  amounts:       { label: "Amounts",       color: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10"},
  locations:     { label: "Locations",     color: "text-sky-400    border-sky-500/30    bg-sky-500/10"      },
  ids:           { label: "IDs",           color: "text-orange-400 border-orange-500/30 bg-orange-500/10"   },
};

const EntityCard = ({ entities }) => {
  const hasEntities = Object.values(entities).some((v) => v?.length > 0);

  return (
    <div className="bg-[#1a1a26] border border-[#2a2a3e] rounded-xl p-5">
      <p className="text-[0.62rem] font-mono uppercase tracking-widest text-[#6b6b88] mb-4">
        Extracted Entities — NER
      </p>

      {!hasEntities ? (
        <p className="text-[0.72rem] font-mono text-[#6b6b88]">
          No named entities detected.
        </p>
      ) : (
        <div className="space-y-3">
          {Object.entries(entities).map(([key, values]) => {
            if (!values?.length) return null;
            const cfg = ENTITY_LABELS[key] ?? {
              label: key,
              color: "text-[#a5a5c0] border-[#2a2a3e] bg-[#12121a]",
            };
            return (
              <div key={key}>
                <p className="text-[0.58rem] font-mono uppercase tracking-widest text-[#6b6b88] mb-1.5">
                  {cfg.label}
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {values.map((v, i) => (
                    <span
                      key={i}
                      className={`text-[0.68rem] font-mono px-2.5 py-0.5 rounded-md border ${cfg.color}`}
                    >
                      {v}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

EntityCard.propTypes = {
  entities: PropTypes.shape({
    persons:       PropTypes.arrayOf(PropTypes.string),
    organizations: PropTypes.arrayOf(PropTypes.string),
    dates:         PropTypes.arrayOf(PropTypes.string),
    amounts:       PropTypes.arrayOf(PropTypes.string),
    locations:     PropTypes.arrayOf(PropTypes.string),
    ids:           PropTypes.arrayOf(PropTypes.string),
  }).isRequired,
};

export default EntityCard;