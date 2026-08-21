import { useState } from "react";

import Header from "./components/Header";
import CompanySelector from "./components/CompanySelector";
import SearchBar from "./components/SearchBar";
import SourceCard from "./components/SourceCard";
import ReactMarkdown from "react-markdown";

function Dashboard() {
  const [ticker, setTicker] = useState("AAPL");
  const [result, setResult] = useState(null);

  return (
    <div className="dashboard">

      <Header />

      <main className="dashboard-content">

        <section className="search-panel">

          <CompanySelector
            ticker={ticker}
            setTicker={setTicker}
          />

          <SearchBar
            ticker={ticker}
            onResults={setResult}
          />

        </section>

        {result && (
          <section className="results">

            {/* AI ANSWER */}

            <div className="answer-card">

              <h2>AI Analysis</h2>

              <div className="answer-text">
                <ReactMarkdown>
                  {result.answer}
                </ReactMarkdown>
              </div>

            </div>


            {/* SOURCES */}

            <div className="sources-section">

              <h2>Sources</h2>

              <p className="sources-description">
                SEC filing information used to generate the answer.
              </p>

              <div className="sources-list">

                {result.sources?.map((source, index) => (
                  <SourceCard
                    key={index}
                    source={source}
                    index={index}
                  />
                ))}

              </div>

            </div>

          </section>
        )}

      </main>

    </div>
  );
}

export default Dashboard;
