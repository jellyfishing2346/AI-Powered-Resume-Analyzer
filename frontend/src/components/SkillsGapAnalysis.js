import React from 'react';

export default function SkillsGapAnalysis({missing=[]}){
  return (
    <div>
      <h4>Skills Gap</h4>
      <ul>
        {missing.length === 0 ? <li>No missing skills detected</li> : missing.map((s,i)=>(<li key={i}>{s}</li>))}
      </ul>
    </div>
  );
}
