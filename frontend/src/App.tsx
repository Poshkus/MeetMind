import { useState } from 'react'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      console.log('Uploading file:', selectedFile.name)
      setSelectedFile(null)
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
            disabled={!selectedFile}
          >
            Upload
          </button>
        </div>
      </main>
    </div>
  )
}

export default App
