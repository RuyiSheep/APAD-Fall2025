import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from './LoadingSpinner';
import API_BASE from './config';

function ProjectManager() {
  const [ownerUserId, setOwnerUserId] = useState('');  // NEW
  const navigate = useNavigate();
  const userId = localStorage.getItem('userId');
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [projectId, setProjectId] = useState('');
  const [existingProjectId, setExistingProjectId] = useState('');
  const [isCreateProjectLoading, setIsCreateProjectLoading] = useState(false);
  const [isJoinProjectLoading, setIsJoinProjectLoading] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('userId');
    navigate('/');
  };

  const handleGoBack = () => {
    navigate(`/dashboard/${userId}`);
  };

const handleCreateProject = () => {
  const owner = ownerUserId || userId; // use typed one or fallback to login

  if (!projectName) {
    alert('Please fill projectName');
    return;
  }
  else if (!projectId){
    alert('Please fill projectId')
  }


  setIsCreateProjectLoading(true);

  fetch(`${API_BASE}/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      projectName,
      projectId,
      description: projectDescription || '',
      ownerUserId: owner,
    }),
  })
    .then(async (res) => {
      const data = await res.json().catch(() => ({}));
      if (!res.ok)
        throw new Error(data.message || data.error || 'Create failed');
      const pid = (data.project && data.project.projectId) || projectId;
      localStorage.setItem('projectId', pid);
      navigate(`/project/${owner}/${encodeURIComponent(pid)}`);
    })
    .catch((err) => {
      alert(err.message);
    })
    .finally(() => {
      setIsCreateProjectLoading(false);
    });
};


  const handleAccessProject = () => {
    if (existingProjectId) {
      setIsJoinProjectLoading(true);
      // Join == add current user to project members
      fetch(`${API_BASE}/projects/${encodeURIComponent(existingProjectId)}/members`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId })
      })
        .then(async res => {
          const data = await res.json().catch(() => ({}));
          if (!res.ok) throw new Error(data.message || data.error || 'Join failed');
          localStorage.setItem('projectId', existingProjectId);
          navigate(`/project/${userId}/${encodeURIComponent(existingProjectId)}`);
        })
        .catch(err => {
          // If already a member, backend may return 409; still allow navigation
          if (String(err.message).toLowerCase().includes('already')) {
            navigate(`/project/${userId}/${encodeURIComponent(existingProjectId)}`);
          } else {
            alert(err.message);
          }
        })
        .finally(() => {
          setIsJoinProjectLoading(false);
        });
    } else {
      alert('Please enter an existing projectId to access.');
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#f4f6f8',
      padding: '20px'
    },
    card: {
      width: '100%',
      maxWidth: '500px',
      backgroundColor: '#fff',
      padding: '30px',
      borderRadius: '8px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
      textAlign: 'center'
    },
    title: {
      fontSize: '24px',
      marginBottom: '20px',
      color: '#333'
    },
    inputGroup: {
      marginBottom: '15px',
      textAlign: 'left'
    },
    label: {
      display: 'block',
      marginBottom: '6px',
      fontSize: '14px',
      color: '#555'
    },
    input: {
      width: '100%',
      padding: '10px',
      borderRadius: '5px',
      border: '1px solid #ddd',
      fontSize: '16px'
    },
    button: {
      width: '100%',
      padding: '12px',
      backgroundColor: '#007bff',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '16px',
      transition: 'background-color 0.3s ease'
    },
    secondaryButton: {
      width: '100%',
      padding: '12px',
      backgroundColor: '#6c757d',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '16px',
      transition: 'background-color 0.3s ease'
    },
    separator: {
      margin: '20px 0',
      borderBottom: '1px solid #eee'
    },
    topBar: {
      display: 'flex',
      justifyContent: 'space-between',
      marginBottom: '10px'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.topBar}>
          <button onClick={handleGoBack} style={styles.secondaryButton}>Back</button>
          <button onClick={handleLogout} style={styles.secondaryButton}>Log out</button>
        </div>

        <h1 style={styles.title}>Project Manager</h1>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Project Name</label>
          <input
            style={styles.input}
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="e.g., Capstone"
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Project ID</label>
          <input
            style={styles.input}
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            placeholder="e.g., proj1"
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Description (optional)</label>
          <input
            style={styles.input}
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
            placeholder="Short description"
          />
        </div>

        <div style={{ marginTop: '10px', marginBottom: '10px' }}>
          {isCreateProjectLoading
            ? <LoadingSpinner />
            : <button style={styles.button} onClick={handleCreateProject}>Create Project</button>}
        </div>

        <div style={styles.separator} />

        <div style={styles.inputGroup}>
          <label style={styles.label}>Access Existing Project (projectId)</label>
          <input
            style={styles.input}
            value={existingProjectId}
            onChange={(e) => setExistingProjectId(e.target.value)}
            placeholder="e.g., proj1"
          />
        </div>
        <div style={styles.inputGroup}>
          <label style={styles.label}>Owner User ID (if not logged in)</label>
          <input
            style={styles.input}
            value={ownerUserId}
            onChange={(e) => setOwnerUserId(e.target.value)}
            placeholder="e.g., u123"
          />
        </div>

        <div style={{ marginTop: '10px' }}>
          {isJoinProjectLoading
            ? <LoadingSpinner />
            : <button style={styles.button} onClick={handleAccessProject}>Join / Open</button>}
        </div>
      </div>
    </div>
  );
}

export default ProjectManager;
