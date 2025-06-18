import { AuthProvider } from './contexts/AuthContext'
import Router from './router'

export default function App() {
  return (
    <AuthProvider>
      <Router />
    </AuthProvider>
  )
}
