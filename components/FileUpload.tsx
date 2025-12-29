
import React, { useRef } from 'react';

interface Props {
  onFilesSelected: (files: File[]) => void;
  isLoading: boolean;
}

export const FileUpload: React.FC<Props> = ({ onFilesSelected, isLoading }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      onFilesSelected(Array.from(e.target.files));
    }
  };

  return (
    <div 
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
        isLoading ? 'bg-gray-50 border-gray-200' : 'bg-indigo-50/50 border-indigo-200 hover:border-indigo-400'
      }`}
    >
      <input
        type="file"
        multiple
        accept=".pdf,.txt,.docx"
        onChange={handleChange}
        ref={fileInputRef}
        className="hidden"
        disabled={isLoading}
      />
      <div className="flex flex-col items-center">
        <svg className="w-12 h-12 text-indigo-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p className="text-gray-600 font-medium">Click to upload resumes</p>
        <p className="text-xs text-gray-400 mt-1">Support PDF, Text, or Word files</p>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isLoading}
          className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400"
        >
          {isLoading ? 'Processing...' : 'Browse Files'}
        </button>
      </div>
    </div>
  );
};