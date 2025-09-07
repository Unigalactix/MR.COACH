import { useContext } from 'react';
import { SyllabusContext } from '../context/SyllabusContext';

export const useSyllabus = () => {
  const context = useContext(SyllabusContext);
  if (!context) {
    throw new Error('useSyllabus must be used within a SyllabusProvider');
  }
  return context;
};
