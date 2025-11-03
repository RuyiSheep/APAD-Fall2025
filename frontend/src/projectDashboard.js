import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import LoadingSpinner from './LoadingSpinner';
import API_BASE from './config';

function ProjectDashboard() {
  const navigate = useNavigate();
  const { userId, projectId } = useParams();
  const [project, setProject] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchProjectDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  const fetchProjectDetails = () => {
    setIsLoading(true);
    fetch(`${API_BASE}/projects/${encodeURIComponent(projectId)}`)
      .then(async res => {
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.message || data.error || 'Failed to fetch project details');
        setProject(data);
      })
      .catch(err => {
        console.error('Error fetching project details:', err);
        alert('Failed to load project details');
        navigate(`/dashboard/${userId}`);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleLogout = () => {
    // localStorage.removeItem('userId');
    localStorage.removeItem('projectId');
    navigate('/');
  };

  const handleGoBack = () => {
    navigate(`/`);
    //navigate(`/dashboard/${userId}`);
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
      maxWidth: '700px',
      backgroundColor: '#fff',
      padding: '30px',
      borderRadius: '8px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
      textAlign: 'left'
    },
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '16px'
    },
    title: { margin: 0 },
    tag: {
      background: '#eef2ff',
      color: '#4338ca',
      padding: '4px 10px',
      borderRadius: '999px',
      fontSize: '12px'
    },
    section: {
      backgroundColor: '#f8f9fa',
      padding: '16px',
      borderRadius: '8px',
      marginBottom: '16px'
    },
    label: { color: '#666', marginBottom: 6 }
  };

  if (isLoading) {
    return (
      <div style={styles.container}>
        <div style={styles.card}><LoadingSpinner /></div>
      </div>
    );
  }

  if (!project) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.header}>
            <h2 style={styles.title}>Project</h2>
            <span className="tag" style={styles.tag}>Not found</span>
          </div>
          <button onClick={handleGoBack}>Back</button>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h2 style={styles.title}>{project.projectName || projectId}</h2>
          <span style={styles.tag}>Project</span>
        </div>

        <div style={styles.section}>
          <div style={styles.label}>Project ID</div>
          <div>{project.projectId}</div>
        </div>

        <div style={styles.section}>
          <div style={styles.label}>Description</div>
          <div>{project.description || '—'}</div>
        </div>

        <div style={styles.section}>
          <div style={styles.label}>Members</div>
          <div>{(project.users || []).length ? project.users.join(', ') : 'none'}</div>
        </div>

        <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
          <button onClick={handleGoBack}>Back</button>
          <button onClick={handleLogout}>Log out</button>
          <button onClick={fetchProjectDetails}>Refresh</button>
        </div>
      </div>
    </div>
  );
}

export default ProjectDashboard;
