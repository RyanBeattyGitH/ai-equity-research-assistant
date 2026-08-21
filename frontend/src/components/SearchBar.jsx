import { useState } from "react";
import { searchFilings } from "../services/api";

function SearchBar({ ticker, onResults }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      console.log("Sending question:", query);
      console.log("Ticker:", ticker);

      // Call the function that actually exists in api.js
      const result = await searchFilings(query, ticker);

      console.log("API response:", result);

      // Send the result back to Dashboard
      onResults(result);
    } catch (err) {
      console.error("Search error:", err);
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !loading) {
            handleSearch();
          }
        }}
        placeholder="Ask a question about this company..."
        disabled={loading}
      />

      <button
        onClick={handleSearch}
        disabled={loading || !query.trim()}
      >
        {loading ? "Generating answer..." : "Ask AI"}
      </button>

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default SearchBar;
