import { useState } from "react";
import ReactMarkdown from "react-markdown";

function SourceCard({ source, index }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <article className="source-card">

      <div className="source-card-header">

        <div className="source-title">
          <h3>Source {index + 1}</h3>
        </div>

        <div className="source-meta">

          {source.ticker && (
            <span className="source-badge">
              {source.ticker}
            </span>
          )}

          {source.form_type && (
            <span className="source-badge">
              {source.form_type}
            </span>
          )}

          {source.filing_year && (
            <span className="source-badge">
              {source.filing_year}
            </span>
          )}

          {source.section && (
            <span className="source-badge">
              {source.section}
            </span>
          )}

        </div>

      </div>

      <div className="source-content">

        <p className="source-label">
          SEC filing excerpt
        </p>

        <div
          className={`source-text ${
            expanded ? "expanded" : ""
          }`}
        >
          <ReactMarkdown
            components={{
              table: ({ children }) => (
                <div className="source-table-wrapper">
                  <table className="source-table">
                    {children}
                  </table>
                </div>
              ),

              thead: ({ children }) => (
                <thead>{children}</thead>
              ),

              tbody: ({ children }) => (
                <tbody>{children}</tbody>
              ),

              tr: ({ children }) => (
                <tr>{children}</tr>
              ),

              th: ({ children }) => (
                <th>{children}</th>
              ),

              td: ({ children }) => (
                <td>{children}</td>
              ),
            }}
          >
            {source.text || source.content || ""}
          </ReactMarkdown>
        </div>

        <button
          className="source-toggle"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? "Show less" : "Show more"}
        </button>

      </div>

    </article>
  );
}

export default SourceCard;
