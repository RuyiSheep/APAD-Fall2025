import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProjectManager from './projectManager';
import ProjectDashboard from './projectDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProjectManager />} />
        <Route path="/project/:userId/:projectId" element={<ProjectDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
