
import { Box, Container, Paper, Typography } from '@mui/material';
import ResumeAnalyzerForm from './ResumeAnalyzerForm';
import CandidateRanking from './CandidateRanking';
import Header from './Header';
import Footer from './Footer';

function App() {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Header />
      <Container maxWidth="md" sx={{ flex: 1, py: 6 }}>
        <Paper elevation={4} sx={{ p: { xs: 2, sm: 5 }, mb: 5, borderRadius: 4, boxShadow: 6 }}>
          <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
            <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f4c8.png" alt="Resume Analyzer Logo" width={64} height={64} style={{ marginBottom: 8 }} />
            <Typography variant="h3" align="center" fontWeight={700} gutterBottom color="primary.dark">
              AI-Powered Resume Analyzer
            </Typography>
            <Typography variant="subtitle1" align="center" color="text.secondary" gutterBottom>
              Upload your resume and job description to get a detailed, AI-driven analysis and candidate ranking.
            </Typography>
          </Box>
        </Paper>
        <ResumeAnalyzerForm />
        <CandidateRanking />
      </Container>
      <Footer />
    </Box>
  );
}

export default App;
