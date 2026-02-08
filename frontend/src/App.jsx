import { useState, useEffect } from 'react';
import {
  Mail,
  TrendingUp,
  Users,
  MessageSquare,
  Sparkles,
  Clock,
  CheckCircle,
  AlertCircle,
  ArrowUpRight,
  Calendar,
  Target,
  Zap,
  BarChart3,
  RefreshCw
} from 'lucide-react';
import Swal from 'sweetalert2';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedLead, setSelectedLead] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/dashboard`);
      const data = await response.json();
      if (data.success) {
        setDashboard(data.data);
      }
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDashboard();
    setTimeout(() => setRefreshing(false), 1000);
  };

  const runAnalysis = async () => {
    // Show beautiful loading state
    Swal.fire({
      title: 'Jarvis is Thinking...',
      text: 'I am analyzing your client documents and market data. Please wait while I generate insights.',
      icon: 'info',
      showConfirmButton: false,
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });

    try {
      const response = await fetch(`${API_URL}/api/run-analysis`, {
        method: 'POST'
      });
      const data = await response.json();

      Swal.fire({
        title: 'Analysis Started!',
        text: 'The agents are now working in the background. Emails will appear shortly.',
        icon: 'success',
        timer: 3000,
        showConfirmButton: false
      });

      // Auto refresh after a delay
      setTimeout(handleRefresh, 5000);

    } catch (error) {
      console.error('Error running analysis:', error);
      Swal.fire('Error', 'Failed to start analysis', 'error');
    }
  };

  const handleActivityClick = (activity) => {
    if (activity.type === 'email_sent' && activity.full_content) {
      Swal.fire({
        title: `Email to ${activity.client}`,
        html: `
          <div style="text-align: left; max-height: 400px; overflow-y: auto;">
            <p><strong>Subject:</strong> ${activity.subject}</p>
            <hr/>
            <div style="white-space: pre-wrap;">${activity.full_content}</div>
          </div>
        `,
        width: '600px',
        confirmButtonText: 'Close'
      });
    } else if (activity.type === 'response_received' && activity.response_text) {
      Swal.fire({
        title: `Response from ${activity.client}`,
        text: activity.response_text,
        icon: 'info'
      });
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading Jarvis Dashboard...</p>
      </div>
    );
  }

  const metrics = dashboard?.metrics || {};
  const warmLeads = dashboard?.warm_leads || [];
  const recentActivity = dashboard?.recent_activity || [];
  const topOpportunities = dashboard?.top_opportunities || [];

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="header-left">
              <div className="logo">
                <Sparkles className="logo-icon" />
                <h1>Jarvis Auto-Pilot</h1>
              </div>
              <p className="tagline">AI that acts FOR you, not just advises</p>
            </div>
            <div className="header-actions">
              {dashboard?.last_analyzed && (
                <span className="last-run">
                  Last analyzed: {formatDate(dashboard.last_analyzed)}
                </span>
              )}
              <button className="btn btn-primary" onClick={runAnalysis} disabled={refreshing}>
                <Zap size={18} className={refreshing ? 'spinning' : ''} />
                {refreshing ? 'Analyzing...' : 'Run Analysis'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">

          {/* Metrics Grid */}
          <div className="metrics-grid">
            <MetricCard
              icon={<Mail />}
              label="Emails Sent Today"
              value={metrics.emails_sent_today || 0}
              trend="+100%"
              color="primary"
            />
            <MetricCard
              icon={<MessageSquare />}
              label="Responses Received"
              value={metrics.responses_received || 0}
              trend={`${metrics.response_rate || 0}% rate`}
              color="success"
            />
            <MetricCard
              icon={<Target />}
              label="Warm Leads Ready"
              value={metrics.warm_leads_count || 0}
              trend="High priority"
              color="warning"
            />
            <MetricCard
              icon={<Users />}
              label="Total Clients"
              value={metrics.total_clients || 0}
              trend="Analyzed"
              color="info"
            />
          </div>

          {/* Warm Leads Section */}
          <section className="section">
            <div className="section-header">
              <div>
                <h2 className="section-title">
                  <Sparkles size={24} />
                  Warm Leads Ready
                </h2>
                <p className="section-subtitle">
                  Jarvis reached out autonomously. These clients responded and are ready for your call.
                </p>
              </div>
            </div>

            <div className="leads-grid">
              {warmLeads.length === 0 ? (
                <div className="empty-state">
                  <AlertCircle size={48} />
                  <h3>No warm leads yet</h3>
                  <p>Run the overnight analysis to generate leads</p>
                  <button className="btn btn-primary" onClick={runAnalysis}>
                    <Zap size={18} />
                    Run Analysis Now
                  </button>
                </div>
              ) : (
                warmLeads.map((lead) => (
                  <LeadCard
                    key={lead.id}
                    lead={lead}
                    onClick={() => setSelectedLead(lead)}
                  />
                ))
              )}
            </div>
          </section>

          {/* Top Opportunities Section */}
          <section className="section">
            <div className="section-header">
              <div>
                <h2 className="section-title">
                  <Zap size={24} className="text-warning" />
                  Jarvis's Top Opportunities
                </h2>
                <p className="section-subtitle">
                  AI-identified high-value outreach opportunities based on deep document analysis.
                </p>
              </div>
            </div>

            <div className="leads-grid shadow-glow-section">
              {topOpportunities.length === 0 ? (
                <div className="empty-state">
                  <Target size={48} />
                  <h3>No opportunities identified yet</h3>
                  <p>Run analysis to let Jarvis find the best targets for you</p>
                </div>
              ) : (
                topOpportunities.map((opp) => (
                  <OpportunityCard
                    key={opp.id}
                    opportunity={opp}
                    onClick={() => {
                      Swal.fire({
                        title: `Opportunity: ${opp.client_name}`,
                        html: `
                          <div style="text-align: left; max-height: 400px; overflow-y: auto;">
                            <div style="background: rgba(99, 102, 241, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                              <p><strong>Opportunity:</strong> ${opp.opportunity_type}</p>
                              <p><strong>Priority Score:</strong> ${opp.priority_score}/10</p>
                            </div>
                            <p><strong>Drafted Outreach:</strong></p>
                            <div style="white-space: pre-wrap; background: #1e293b; padding: 15px; border-radius: 8px; font-size: 0.9em; color: #e2e8f0; border: 1px solid #334155;">${opp.full_content || opp.body}</div>
                          </div>
                        `,
                        width: '600px',
                        confirmButtonText: 'Great, let\'s go!',
                        showCancelButton: true,
                        cancelButtonText: 'Close'
                      });
                    }}
                  />
                ))
              )}
            </div>
          </section>

          {/* Recent Activity */}
          <section className="section">
            <div className="section-header">
              <h2 className="section-title">
                <Clock size={24} />
                Recent Activity
              </h2>
            </div>

            <div className="activity-list">
              {recentActivity.slice(0, 10).map((activity, index) => (
                <ActivityItem
                  key={index}
                  activity={activity}
                  onClick={() => handleActivityClick(activity)}
                />
              ))}
            </div>
          </section>

        </div>
      </main>

      {/* Lead Detail Modal */}
      {selectedLead && (
        <LeadDetailModal
          lead={selectedLead}
          onClose={() => setSelectedLead(null)}
        />
      )}
    </div>
  );
}

// Metric Card Component
function MetricCard({ icon, label, value, trend, color }) {
  return (
    <div className={`metric-card metric-card-${color}`}>
      <div className="metric-icon">{icon}</div>
      <div className="metric-content">
        <p className="metric-label">{label}</p>
        <h3 className="metric-value">{value}</h3>
        <p className="metric-trend">
          <TrendingUp size={14} />
          {trend}
        </p>
      </div>
    </div>
  );
}

// Opportunity Card Component
function OpportunityCard({ opportunity, onClick }) {
  return (
    <div className="lead-card opportunity-card" onClick={onClick}>
      <div className="lead-card-header">
        <div>
          <h3 className="lead-name">{opportunity.client_name}</h3>
          <p className="lead-company">{opportunity.client_email}</p>
        </div>
        <div className="lead-badges">
          <span className={`badge badge-danger`}>
            Priority {opportunity.priority_score}/10
          </span>
          <span className={`badge badge-primary`}>
            {opportunity.tone || 'Professional'}
          </span>
        </div>
      </div>

      <div className="lead-card-body">
        <div className="opportunity-type">
          <p className="response-label">Target Opportunity:</p>
          <p className="opportunity-text">{opportunity.opportunity_type}</p>
        </div>

        <div className="email-preview-snippet">
          <p className="response-label">Suggested Outreach:</p>
          <p className="response-text">"{opportunity.preview || (opportunity.body ? opportunity.body.substring(0, 100) + '...' : '')}"</p>
        </div>
      </div>

      <div className="lead-card-footer">
        <div className="engagement-score">
          <Sparkles size={14} />
          AI Analysis Complete
        </div>
        <ArrowUpRight size={16} className="arrow-icon" />
      </div>
    </div>
  );
}

// Lead Card Component
function LeadCard({ lead, onClick }) {
  const priorityColors = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  };

  const sentimentColors = {
    positive: 'success',
    neutral: 'info',
    negative: 'danger'
  };

  return (
    <div className="lead-card" onClick={onClick}>
      <div className="lead-card-header">
        <div>
          <h3 className="lead-name">{lead.client_name}</h3>
          <p className="lead-company">{lead.company}</p>
        </div>
        <div className="lead-badges">
          <span className={`badge badge-${priorityColors[lead.priority]}`}>
            {lead.priority} priority
          </span>
          <span className={`badge badge-${sentimentColors[lead.sentiment]}`}>
            {lead.sentiment}
          </span>
        </div>
      </div>

      <div className="lead-card-body">
        <div className="lead-timeline">
          <div className="timeline-item">
            <CheckCircle size={16} className="timeline-icon success" />
            <div>
              <p className="timeline-label">Jarvis sent email</p>
              <p className="timeline-time">{formatDate(lead.email_sent)}</p>
            </div>
          </div>
          <div className="timeline-item">
            <MessageSquare size={16} className="timeline-icon primary" />
            <div>
              <p className="timeline-label">Client responded</p>
              <p className="timeline-time">{formatDate(lead.response_received)}</p>
            </div>
          </div>
        </div>

        <div className="lead-response">
          <p className="response-label">Client's Response:</p>
          <p className="response-text">"{lead.response_text.substring(0, 150)}..."</p>
        </div>

        <div className="lead-action">
          <button className="btn btn-primary btn-block">
            <Target size={16} />
            {lead.next_action}
          </button>
        </div>
      </div>

      <div className="lead-card-footer">
        <div className="engagement-score">
          <BarChart3 size={14} />
          Engagement: {lead.engagement_score}/100
        </div>
        <ArrowUpRight size={16} className="arrow-icon" />
      </div>
    </div>
  );
}

// Activity Item Component
function ActivityItem({ activity, onClick }) {
  const getIcon = () => {
    if (activity.type === 'email_sent') {
      return <Mail size={16} className="activity-icon primary" />;
    }
    return <MessageSquare size={16} className="activity-icon success" />;
  };

  const getSentimentBadge = () => {
    if (!activity.sentiment) return null;
    const colors = {
      positive: 'success',
      neutral: 'info',
      negative: 'danger'
    };
    return <span className={`badge badge-${colors[activity.sentiment]}`}>{activity.sentiment}</span>;
  };

  return (
    <div className="activity-item clickable" onClick={onClick} style={{ cursor: 'pointer' }}>
      {getIcon()}
      <div className="activity-content">
        <p className="activity-description">{activity.description}</p>
        {activity.subject && <p className="activity-subject">{activity.subject}</p>}
      </div>
      <div className="activity-meta">
        {getSentimentBadge()}
        <span className="activity-time">{formatDate(activity.timestamp)}</span>
      </div>
    </div>
  );
}

// Lead Detail Modal Component

// Lead Detail Modal Component
function LeadDetailModal({ lead, onClose }) {
  const [activeTab, setActiveTab] = useState('context');

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-group">
            <h2>🎯 Warm Lead: {lead.client_name}</h2>
            <span className={`badge badge-${lead.sentiment === 'positive' ? 'success' : 'info'}`}>
              {lead.sentiment} Interest
            </span>
          </div>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-tabs">
          <button
            className={`tab-btn ${activeTab === 'context' ? 'active' : ''}`}
            onClick={() => setActiveTab('context')}
          >
            Client Context
          </button>
          <button
            className={`tab-btn ${activeTab === 'email' ? 'active' : ''}`}
            onClick={() => setActiveTab('email')}
          >
            Sent Email
          </button>
        </div>

        <div className="modal-body">
          {activeTab === 'context' ? (
            <>
              <div className="modal-section">
                <h3>Client Information</h3>
                <div className="info-grid">
                  <div className="info-item">
                    <span className="info-label">Company:</span>
                    <span className="info-value">{lead.company}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Industry:</span>
                    <span className="info-value">{lead.industry}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Email:</span>
                    <span className="info-value">{lead.client_email}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Engagement Score:</span>
                    <span className="info-value">{lead.engagement_score}/100</span>
                  </div>
                </div>
              </div>

              <div className="modal-section">
                <h3>Client's Response</h3>
                <div className="response-preview">
                  <p>"{lead.response_text}"</p>
                  <div className="response-meta">
                    <span className="response-time">Received {formatDate(lead.response_received)}</span>
                  </div>
                </div>
              </div>

              <div className="modal-section">
                <h3>Context from Client Documents</h3>
                <div className="context-section">
                  <h4>Key Insights:</h4>
                  <ul className="context-list">
                    {lead.context?.key_insights?.map((insight, i) => (
                      <li key={i}>{insight}</li>
                    ))}
                  </ul>
                  <h4>Pain Points:</h4>
                  <ul className="context-list">
                    {lead.context?.pain_points?.map((pain, i) => (
                      <li key={i}>{pain}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </>
          ) : (
            <div className="modal-section">
              <h3>Email Sent by Jarvis</h3>
              <div className="email-full-view">
                <div className="email-header-meta">
                  <p><strong>To:</strong> {lead.client_email}</p>
                  <p><strong>Subject:</strong> {lead.email_subject}</p>
                  <p><strong>Sent:</strong> {formatDate(lead.email_sent)}</p>
                </div>
                <div className="email-body-content">
                  {lead.email_body ? (
                    lead.email_body.split('\n').map((line, i) => (
                      <p key={i}>{line || <br />}</p>
                    ))
                  ) : (
                    <p className="text-muted">No email content available.</p>
                  )}
                </div>
              </div>
            </div>
          )}

          <div className="modal-actions">
            <button
              className="btn btn-primary btn-large"
              onClick={() => {
                Swal.fire({
                  title: 'Redirecting to Slack...',
                  text: 'Opening scheduling interface with client context...',
                  icon: 'success',
                  timer: 2000,
                  showConfirmButton: false
                });
              }}
            >
              <Calendar size={20} />
              Schedule Meeting
            </button>
            <button className="btn btn-outline btn-large">
              <Target size={20} />
              {lead.next_action}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <Sparkles size={16} />
            <span>Jarvis Auto-Pilot</span>
          </div>
          <div className="footer-links">
            <span>Powered by Google Gemini</span>
            <span>•</span>
            <span>LangGraph Agentic Framework</span>
            <span>•</span>
            <span>v2.0.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

// Utility Functions
function formatDate(dateString) {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  
  if (diffMs < 0) return 'Just now';
  
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export default App;
