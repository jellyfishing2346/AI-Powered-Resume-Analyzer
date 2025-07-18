import React, { useState } from 'react';
import { Box, Button, Typography, TextField, Paper, Grid, CircularProgress, Alert, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://ai-powered-resume-analyzer-1-i3r9.onrender.com';

function ResumeAnalyzerForm() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [endpoint, setEndpoint] = useState('analyze_resume'); // default endpoint

  const handleFileChange = (e) => {
    setResume(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');
  setResult(null);
  if (!resume || !jobDescription) {
    setError('Please upload a resume and enter a job description.');
    return;
  }
  setLoading(true);
  try {
    const formData = new FormData();
    if (endpoint === 'analyze_resume') {
      formData.append('file', resume); // backend expects 'file'
    } else if (endpoint === 'match_resume') {
      formData.append('resume', resume); // backend expects 'resume'
      formData.append('job_description', jobDescription);
    }
    const url = `${API_BASE}/${endpoint}/`;
    const response = await axios.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    setResult(response.data);
  } catch (err) {
    setError(err.response?.data?.detail || 'Failed to analyze resume. Please try again.');
    console.error('API Error:', err);
  } finally {
    setLoading(false);
  }
};

  return (
    <Paper elevation={3} sx={{ p: { xs: 2, sm: 4 }, mb: 5, borderRadius: 3, boxShadow: 4, background: 'rgba(255,255,255,0.98)' }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Button
              variant="contained"
              component="label"
              fullWidth
              sx={{ py: 1.5, fontWeight: 600, fontSize: '1.1rem', borderRadius: 2, boxShadow: 2 }}
            >
              Upload Resume (PDF, DOCX, TXT)
              <input type="file" hidden onChange={handleFileChange} accept=".pdf,.doc,.docx,.txt" />
            </Button>
            {resume && <Typography variant="body2" sx={{ mt: 1, color: 'primary.main', fontWeight: 500 }}>{resume.name}</Typography>}
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
            <FormControl component="fieldset">
              <FormLabel component="legend">Analysis Type</FormLabel>
              <RadioGroup
                row
                value={endpoint}
                onChange={(e) => setEndpoint(e.target.value)}
              >
                <FormControlLabel value="analyze_resume" control={<Radio />} label="Analyze Resume" />
                <FormControlLabel value="match_resume" control={<Radio />} label="Match Resume to Job" />
              </RadioGroup>
            </FormControl>
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
              {loading ? <CircularProgress size={24} /> : 'Analyze Resume'}
            </Button>
          </Grid>
        </Grid>
      </form>
      {error && <Alert severity="error" sx={{ mt: 3 }}>{error}</Alert>}
      {result && result.analysis && (
        <Box sx={{ mt: 5 }}>
          <Typography variant="h5" gutterBottom color="primary.dark" fontWeight={600}>Analysis Results</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Paper variant="outlined" sx={{ p: 2, mb: 2, background: '#f5f7fa', borderRadius: 2 }}>
                <Typography variant="subtitle1"><b>Match Score:</b> {result.analysis.match_score ? (result.analysis.match_score * 100).toFixed(1) + '%' : 'N/A'}</Typography>
                <Typography variant="subtitle1" sx={{ mt: 1 }}><b>Word Count:</b> {result.analysis.word_count}</Typography>
                <Typography variant="subtitle1" sx={{ mt: 1 }}><b>Skills Found:</b> {result.analysis.skill_count}</Typography>
                <Typography variant="subtitle1" sx={{ mt: 1 }}><b>Entities:</b> {result.analysis.entities?.length || 0}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Paper variant="outlined" sx={{ p: 2, mb: 2, background: '#f5f7fa', borderRadius: 2 }}>
                <Typography variant="subtitle1"><b>File:</b> {result.filename}</Typography>
                <Typography variant="subtitle1" sx={{ mt: 1 }}><b>File Size:</b> {result.metadata?.file_size} characters</Typography>
                <Typography variant="subtitle1" sx={{ mt: 1 }}><b>Status:</b> {result.success ? 'Success' : 'Failed'}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ mt: 2, fontWeight: 600 }}><b>Skills Found:</b></Typography>
              <Paper variant="outlined" sx={{ p: 2, mt: 1, maxHeight: 150, overflow: 'auto', background: '#fafafa', borderRadius: 2 }}>
                <Typography variant="body2">
                  {result.analysis.skills?.length > 0 ? result.analysis.skills.join(', ') : 'No skills detected'}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ mt: 2, fontWeight: 600 }}><b>Named Entities:</b></Typography>
              <Paper variant="outlined" sx={{ p: 2, mt: 1, maxHeight: 200, overflow: 'auto', background: '#fafafa', borderRadius: 2 }}>
                {result.analysis.entities?.slice(0, 10).map((entity, index) => (
                  <Typography key={index} variant="body2" sx={{ mb: 0.5 }}>
                    <b>{entity.label}:</b> {entity.text.trim()} <em>({entity.description})</em>
                  </Typography>
                )) || <Typography variant="body2">No entities detected</Typography>}
                {result.analysis.entities?.length > 10 && (
                  <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
                    ... and {result.analysis.entities.length - 10} more entities
                  </Typography>
                )}
              </Paper>
            </Grid>
          </Grid>
        </Box>
      )}
    </Paper>
  );
}

export default ResumeAnalyzerForm;