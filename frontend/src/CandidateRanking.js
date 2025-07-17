import React, { useState } from 'react';
import { 
  Box, Button, Typography, TextField, Paper, Grid, CircularProgress, Alert, 
  List, ListItem, ListItemText, Divider, LinearProgress, Chip, Accordion,
  AccordionSummary, AccordionDetails, Card, CardContent 
} from '@mui/material';
import { ExpandMore, TrendingUp, Person, Assessment } from '@mui/icons-material';
import axios from 'axios';

// ...existing imports...

const API_BASE = process.env.REACT_APP_API_URL || 'https://ai-powered-resume-analyzer-1-i3r9.onrender.com';

function CandidateRanking() {
  const [resumes, setResumes] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setResumes(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResults(null);
    if (!resumes.length || !jobDescription) {
      setError('Please upload at least one resume and enter a job description.');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      resumes.forEach((file) => formData.append('resumes', file));
      formData.append('job_description', jobDescription);
      console.log('Request URL:', `${API_BASE}/rank_candidates/`);
      for (let pair of formData.entries()) {
        console.log(pair[0]+ ':', pair[1]);
  }
      const response = await axios.post(`${API_BASE}/rank_candidates/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      // Defensive: check if ranked_candidates exists and is an array
      if (response.data && Array.isArray(response.data.ranked_candidates)) {
        // Map backend fields to frontend expectations
        const mappedResults = response.data.ranked_candidates.map((c, idx) => ({
          ...c,
          match_score: c.skill_match_percentage ?? 0,
          skill_count: c.matched_skills?.length ?? 0,
          word_count: c.preview ? c.preview.split(/\s+/).length : 0,
          entity_count: c.matched_skills?.length ?? 0,
          resume_preview: c.preview ?? '',
          rank: idx + 1,
          skills: c.matched_skills ?? [],
        }));
        setResults(mappedResults);
      } else {
        setError('Unexpected response format from server.');
        setResults([]);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Failed to rank candidates. Please try again.'
      );
      setResults([]);
      console.error('Ranking error:', err);
    } finally {
      setLoading(false);
    }
  };

  // ...rest of your component unchanged...

  return (
    <Paper elevation={3} sx={{ p: { xs: 2, sm: 4 }, mb: 5, borderRadius: 3, boxShadow: 4, background: 'rgba(255,255,255,0.98)' }}>
      <Typography variant="h5" gutterBottom color="primary.dark" fontWeight={600}>Candidate Ranking</Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Button
              variant="contained"
              component="label"
              fullWidth
              sx={{ py: 1.5, fontWeight: 600, fontSize: '1.1rem', borderRadius: 2, boxShadow: 2 }}
            >
              Upload Resumes (PDF, DOCX, TXT, multiple allowed)
              <input type="file" hidden multiple onChange={handleFileChange} accept=".pdf,.doc,.docx,.txt" />
            </Button>
            {resumes.length > 0 && (
              <Typography variant="body2" sx={{ mt: 1, color: 'primary.main', fontWeight: 500 }}>{resumes.map(f => f.name).join(', ')}</Typography>
            )}
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Job Description"
              multiline
              minRows={4}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              fullWidth
              required
              sx={{ background: '#f7fafd', borderRadius: 2 }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              disabled={loading}
              sx={{ py: 1.3, fontWeight: 700, fontSize: '1.1rem', borderRadius: 2, boxShadow: 2, transition: '0.2s', ':hover': { background: 'primary.dark' } }}
            >
              {loading ? <CircularProgress size={24} /> : 'Rank Candidates'}
            </Button>
          </Grid>
        </Grid>
      </form>
      {error && <Alert severity="error" sx={{ mt: 3 }}>{error}</Alert>}
      {results && (
        <Box sx={{ mt: 5 }}>
          <Typography variant="h6" gutterBottom color="primary.dark" fontWeight={600}>
            🏆 Ranked Candidates ({results.length} total)
          </Typography>
          
          {/* Summary Stats */}
          <Card sx={{ mb: 3, background: 'linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%)' }}>
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <TrendingUp color="primary" sx={{ fontSize: 40 }} />
                    <Typography variant="h6" color="primary.main">
                      {(results[0]?.match_score * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2">Top Match</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Person color="primary" sx={{ fontSize: 40 }} />
                    <Typography variant="h6" color="primary.main">
                      {results.length}
                    </Typography>
                    <Typography variant="body2">Candidates</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Assessment color="primary" sx={{ fontSize: 40 }} />
                    <Typography variant="h6" color="primary.main">
                      {Math.round(results.reduce((acc, r) => acc + r.skill_count, 0) / results.length)}
                    </Typography>
                    <Typography variant="body2">Avg Skills</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Candidate List */}
          <List>
            {results.map((candidate, idx) => {
              const matchPercentage = candidate.match_score * 100;
              const getRankColor = (rank) => {
                if (rank === 1) return '#FFD700'; // Gold
                if (rank === 2) return '#C0C0C0'; // Silver  
                if (rank === 3) return '#CD7F32'; // Bronze
                return '#e0e0e0'; // Default
              };
              
              return (
                <Accordion key={candidate.filename} sx={{ mb: 2 }}>
                  <AccordionSummary 
                    expandIcon={<ExpandMore />}
                    sx={{ 
                      background: `linear-gradient(90deg, ${getRankColor(candidate.rank)}15 0%, transparent 100%)`,
                      borderLeft: `4px solid ${getRankColor(candidate.rank)}`
                    }}
                  >
                    <Box sx={{ width: '100%' }}>
                      <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                        <Typography variant="h6" fontWeight={700}>
                          #{candidate.rank} {candidate.filename}
                        </Typography>
                        <Chip 
                          label={`${matchPercentage.toFixed(1)}% match`} 
                          color={matchPercentage > 60 ? 'success' : matchPercentage > 40 ? 'warning' : 'default'}
                          variant="filled"
                        />
                      </Box>
                      
                      {/* Match Score Progress Bar */}
                      <Box sx={{ width: '100%', mb: 1 }}>
                        <Box display="flex" justifyContent="space-between" mb={0.5}>
                          <Typography variant="body2" color="text.secondary">Match Score</Typography>
                          <Typography variant="body2" color="text.secondary">{matchPercentage.toFixed(1)}%</Typography>
                        </Box>
                        <LinearProgress 
                          variant="determinate" 
                          value={matchPercentage} 
                          sx={{ 
                            height: 8, 
                            borderRadius: 4,
                            backgroundColor: '#e0e0e0',
                            '& .MuiLinearProgress-bar': {
                              borderRadius: 4,
                              backgroundColor: matchPercentage > 60 ? '#4caf50' : matchPercentage > 40 ? '#ff9800' : '#f44336'
                            }
                          }}
                        />
                      </Box>
                      
                      <Typography variant="body2" color="text.secondary">
                        {candidate.skill_count} skills • {candidate.word_count} words • {candidate.entity_count} entities
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  
                  <AccordionDetails>
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={6}>
                        <Typography variant="subtitle2" gutterBottom fontWeight={600}>
                          🎯 Top Skills Found
                        </Typography>
                        <Box sx={{ mb: 2 }}>
                          {candidate.skills.slice(0, 10).map((skill, skillIdx) => (
                            <Chip 
                              key={skillIdx} 
                              label={skill} 
                              size="small" 
                              sx={{ mr: 0.5, mb: 0.5 }}
                              color={skillIdx < 5 ? 'primary' : 'default'}
                              variant={skillIdx < 3 ? 'filled' : 'outlined'}
                            />
                          ))}
                          {candidate.skills.length > 10 && (
                            <Chip 
                              label={`+${candidate.skills.length - 10} more`} 
                              size="small" 
                              variant="outlined"
                            />
                          )}
                        </Box>
                      </Grid>
                      
                      <Grid item xs={12} md={6}>
                        <Typography variant="subtitle2" gutterBottom fontWeight={600}>
                          📊 Analysis Summary
                        </Typography>
                        <Box sx={{ p: 2, background: '#f5f5f5', borderRadius: 2 }}>
                          <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>File:</strong> {candidate.filename}
                          </Typography>
                          <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>Match Score:</strong> {matchPercentage.toFixed(1)}%
                          </Typography>
                          <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>Skills Found:</strong> {candidate.skill_count}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Entities:</strong> {candidate.entity_count}
                          </Typography>
                        </Box>
                      </Grid>
                      
                      <Grid item xs={12}>
                        <Typography variant="subtitle2" gutterBottom fontWeight={600}>
                          📄 Resume Preview
                        </Typography>
                        <Paper variant="outlined" sx={{ p: 2, maxHeight: 150, overflow: 'auto', background: '#fafafa' }}>
                          <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
                            {candidate.resume_preview}
                          </Typography>
                        </Paper>
                      </Grid>
                    </Grid>
                  </AccordionDetails>
                </Accordion>
              );
            })}
          </List>
          
          {/* Action Buttons */}
          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button 
              variant="outlined" 
              onClick={() => window.print()}
              sx={{ minWidth: 120 }}
            >
              📄 Print Results
            </Button>
            <Button 
              variant="contained" 
              onClick={() => {
                const dataStr = JSON.stringify(results, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'candidate_ranking_results.json';
                link.click();
              }}
              sx={{ minWidth: 120 }}
            >
              💾 Download Results
            </Button>
          </Box>
        </Box>
      )}
    </Paper>
  );
}

export default CandidateRanking;
