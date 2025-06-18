import RegistrationForm from '../components/auth/RegistrationForm'
import ToggleThemeButton from '../components/ToggleThemeButton'

export default function RegistrationPage() {
  return (
    <div className="registration-page">
      <ToggleThemeButton />
      <RegistrationForm />
    </div>
  )
}