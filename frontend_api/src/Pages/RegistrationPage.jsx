import RegistrationForm from '../components/Auth/RegistrationForm'
import ToggleThemeButton from '../components/ToggleThemeButton'

export default function RegistrationPage() {
  return (
    <div className="registration-page">
      <ToggleThemeButton />
      <RegistrationForm />
    </div>
  )
}