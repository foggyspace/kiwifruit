import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./styles/reset.less"
import "./styles/common.less"
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
