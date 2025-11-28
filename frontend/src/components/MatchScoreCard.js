import React from 'react';

export default function MatchScoreCard({score=0, title='Match'}){
  return (
    <div style={{border:'1px solid #ddd', padding:12, borderRadius:6}}>
      <h4>{title}</h4>
      <div style={{fontSize:22, fontWeight:700}}>{score}%</div>
    </div>
  );
}
