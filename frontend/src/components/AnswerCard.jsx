function AnswerCard({ answer }) {
  if (!answer) {
    return null;
  }

  return (
    <section className="answer-card">
      <div className="section-header">
        <h2>AI Analysis</h2>
      </div>

      <div className="answer-content">
        <p>{answer}</p>
      </div>
    </section>
  );
}

export default AnswerCard;
