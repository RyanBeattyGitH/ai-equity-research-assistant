import React from "react";

const companies = [
  {
    ticker: "AAPL",
    name: "Apple",
  },
  {
    ticker: "JPM",
    name: "JPMorgan Chase",
  },
];

function CompanySelector({ ticker, setTicker }) {
  return (
    <div className="company-selector">
      <label htmlFor="company">Company</label>

      <select
        id="company"
        value={ticker}
        onChange={(event) => setTicker(event.target.value)}
      >
        {companies.map((company) => (
          <option key={company.ticker} value={company.ticker}>
            {company.name} ({company.ticker})
          </option>
        ))}
      </select>
    </div>
  );
}

export default CompanySelector;
