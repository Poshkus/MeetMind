import { useState } from 'react'
import { toast } from 'react-hot-toast'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
      const response = await fetch(`${backendUrl}/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`)
      }

      const result = await response.json()
      toast.success(`Upload successful! Transcription: ${result.transcription}`)
      setSelectedFile(null)
    } catch (err: any) {
      toast.error(err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="navbar-container">
          <div className="logo">MeetMind</div>
          <button className="login-btn">Login</button>
        </div>
      </nav>

      <main className="main-section">
        <div className="upload-card">
          <h2 className="card-title">Upload Meeting</h2>

          <label className="file-input-wrapper">
            <input
              type="file"
              accept="audio/*,video/*"
              onChange={handleFileChange}
              className="file-input"
            />
            <span className="file-input-label">
              {selectedFile ? selectedFile.name : 'Choose audio or video file'}
            </span>
          </label>

          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </main>
    </div>
  )
}

export default App