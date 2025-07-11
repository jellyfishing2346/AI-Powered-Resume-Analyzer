import React from 'react';
import { Box, Typography, Link } from '@mui/material';

function Footer() {
  return (
    <Box component="footer" sx={{ mt: 8, py: 3, textAlign: 'center', color: 'text.secondary', background: 'rgba(245, 247, 250, 0.7)', borderTop: '1px solid #e0e0e0' }}>
      <Typography variant="body2">
        © {new Date().getFullYear()} AI-Powered Resume Analyzer &nbsp;|&nbsp;
        <Link href="https://github.com/jellyfishing2346/AI-Powered-Resume-Analyzer" target="_blank" rel="noopener" underline="hover">
          GitHub
        </Link>
        &nbsp;|&nbsp;
        <Link href="mailto:faizanakhan2003@gmail.com" underline="hover">Contact</Link>
      </Typography>
    </Box>
  );
}

export default Footer;
