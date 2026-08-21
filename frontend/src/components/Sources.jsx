import React from "react";
import SourceCard from "./SourceCard";

function Sources({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <section className="sources-section">
      <h2>Sources</h2>

      <div className="sources">
        {sources.map((source, index) => (
          <SourceCard
            key={`${source.ticker}-${source.filing_year}-${index}`}
            source={source}
          />
        ))}
      </div>
    </section>
  );
}

export default Sources;
