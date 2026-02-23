import { FormEvent, useEffect, useMemo, useState } from 'react';

type Workspace = {
  id: number;
  name: string;
  description?: string | null;
};

type SearchResult = {
  external_id?: string | null;
  title: string;
  authors: string[];
  published_date?: string | null;
  abstract?: string | null;
  source: string;
};

type ImportedPaper = {
  id: number;
  workspace_id: number;
  title: string;
  authors?: string | null;
  abstract?: string | null;
  source: string;
};

type ChatResponse = {
  answer: string;
  references: string[];
};

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function apiRequest<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers ?? {})
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? 'Request failed');
  }

  return response.json() as Promise<T>;
}

export function App() {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [error, setError] = useState<string>('');

  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState<number | null>(null);
  const [workspaceName, setWorkspaceName] = useState('');
  const [workspaceDescription, setWorkspaceDescription] = useState('');

  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [papers, setPapers] = useState<ImportedPaper[]>([]);

  const [message, setMessage] = useState('');
  const [chat, setChat] = useState<ChatResponse | null>(null);
  const [busy, setBusy] = useState(false);

  const isAuthed = useMemo(() => Boolean(token), [token]);

  useEffect(() => {
    if (!token) return;
    void loadWorkspaces(token);
  }, [token]);

  useEffect(() => {
    if (!token || !selectedWorkspace) return;
    void loadWorkspacePapers(token, selectedWorkspace);
  }, [token, selectedWorkspace]);

  async function loadWorkspaces(authToken: string) {
    const data = await apiRequest<Workspace[]>('/workspaces', { method: 'GET' }, authToken);
    setWorkspaces(data);
    if (!selectedWorkspace && data.length > 0) {
      setSelectedWorkspace(data[0].id);
    }
  }

  async function loadWorkspacePapers(authToken: string, workspaceId: number) {
    const data = await apiRequest<ImportedPaper[]>(`/workspaces/${workspaceId}/papers`, { method: 'GET' }, authToken);
    setPapers(data);
  }

  async function handleAuth(event: FormEvent) {
    event.preventDefault();
    setError('');
    setBusy(true);
    try {
      if (mode === 'register') {
        await apiRequest('/auth/register', {
          method: 'POST',
          body: JSON.stringify({ email, password, full_name: fullName })
        });
        setMode('login');
      } else {
        const data = await apiRequest<{ access_token: string }>('/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email, password })
        });
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setBusy(false);
    }
  }

  async function handleCreateWorkspace(event: FormEvent) {
    event.preventDefault();
    if (!token) return;
    setBusy(true);
    setError('');
    try {
      await apiRequest<Workspace>(
        '/workspaces',
        {
          method: 'POST',
          body: JSON.stringify({ name: workspaceName, description: workspaceDescription })
        },
        token
      );
      setWorkspaceName('');
      setWorkspaceDescription('');
      await loadWorkspaces(token);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed creating workspace');
    } finally {
      setBusy(false);
    }
  }

  async function handleSearch(event: FormEvent) {
    event.preventDefault();
    if (!token) return;
    setBusy(true);
    setError('');
    try {
      const data = await apiRequest<SearchResult[]>(
        '/papers/search',
        {
          method: 'POST',
          body: JSON.stringify({ query, max_results: 8 })
        },
        token
      );
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setBusy(false);
    }
  }

  async function handleImportPaper(paper: SearchResult) {
    if (!token || !selectedWorkspace) return;
    setBusy(true);
    setError('');
    try {
      await apiRequest(
        '/papers/import',
        {
          method: 'POST',
          body: JSON.stringify({ workspace_id: selectedWorkspace, paper })
        },
        token
      );
      await loadWorkspacePapers(token, selectedWorkspace);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Import failed');
    } finally {
      setBusy(false);
    }
  }

  async function handleChat(event: FormEvent) {
    event.preventDefault();
    if (!token || !selectedWorkspace) return;
    setBusy(true);
    setError('');
    try {
      const data = await apiRequest<ChatResponse>(
        '/chat',
        {
          method: 'POST',
          body: JSON.stringify({ workspace_id: selectedWorkspace, message })
        },
        token
      );
      setChat(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Chat failed');
    } finally {
      setBusy(false);
    }
  }

  function logout() {
    localStorage.removeItem('token');
    setToken(null);
    setWorkspaces([]);
    setSelectedWorkspace(null);
    setResults([]);
    setPapers([]);
    setChat(null);
  }

  if (!isAuthed) {
    return (
      <main className="page auth-page">
        <section className="card auth-card">
          <h1>ResearchHub</h1>
          <p className="muted">AI-powered research discovery and chat</p>
          <form onSubmit={handleAuth} className="stack">
            {mode === 'register' && (
              <input
                required
                placeholder="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            )}
            <input required type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input
              required
              minLength={6}
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button disabled={busy}>{busy ? 'Please wait...' : mode === 'login' ? 'Login' : 'Register'}</button>
          </form>
          <button className="ghost" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
            {mode === 'login' ? 'Need an account? Register' : 'Already have an account? Login'}
          </button>
          {error && <p className="error">{error}</p>}
        </section>
      </main>
    );
  }

  return (
    <main className="page">
      <header className="topbar">
        <div>
          <h1>ResearchHub Console</h1>
          <p className="muted">Minimal black/white frontend for your FastAPI backend</p>
        </div>
        <button className="ghost" onClick={logout}>
          Logout
        </button>
      </header>

      {error && <p className="error">{error}</p>}

      <section className="grid">
        <article className="card">
          <h2>Workspaces</h2>
          <form onSubmit={handleCreateWorkspace} className="stack compact">
            <input
              required
              placeholder="Workspace name"
              value={workspaceName}
              onChange={(e) => setWorkspaceName(e.target.value)}
            />
            <textarea
              placeholder="Description"
              value={workspaceDescription}
              onChange={(e) => setWorkspaceDescription(e.target.value)}
            />
            <button disabled={busy}>Create workspace</button>
          </form>

          <div className="list">
            {workspaces.map((workspace) => (
              <button
                key={workspace.id}
                onClick={() => setSelectedWorkspace(workspace.id)}
                className={selectedWorkspace === workspace.id ? 'selected' : ''}
              >
                <strong>{workspace.name}</strong>
                <span>{workspace.description || 'No description'}</span>
              </button>
            ))}
            {workspaces.length === 0 && <p className="muted">No workspaces yet.</p>}
          </div>
        </article>

        <article className="card">
          <h2>Search & Import Papers</h2>
          <form onSubmit={handleSearch} className="stack compact">
            <input
              required
              placeholder="Search arXiv topic..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button disabled={busy || !selectedWorkspace}>Search</button>
          </form>

          <div className="list tall">
            {results.map((paper) => (
              <div key={`${paper.external_id ?? 'none'}-${paper.title}`} className="panel">
                <h3>{paper.title}</h3>
                <p className="muted small">{paper.authors.join(', ')}</p>
                <p className="small">{paper.abstract?.slice(0, 220) || 'No abstract available'}...</p>
                <button disabled={!selectedWorkspace || busy} onClick={() => void handleImportPaper(paper)}>
                  Import
                </button>
              </div>
            ))}
          </div>
        </article>

        <article className="card">
          <h2>Workspace Papers & AI Chat</h2>
          <p className="muted small">Imported papers: {papers.length}</p>
          <ul className="paper-list">
            {papers.map((paper) => (
              <li key={paper.id}>{paper.title}</li>
            ))}
          </ul>

          <form onSubmit={handleChat} className="stack compact">
            <textarea
              required
              placeholder="Ask a question about your imported papers"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
            <button disabled={busy || !selectedWorkspace}>Ask AI</button>
          </form>

          {chat && (
            <div className="panel response">
              <h3>Answer</h3>
              <p>{chat.answer}</p>
              <h4>References</h4>
              <ul>
                {chat.references.map((reference) => (
                  <li key={reference}>{reference}</li>
                ))}
              </ul>
            </div>
          )}
        </article>
      </section>
    </main>
  );
}
