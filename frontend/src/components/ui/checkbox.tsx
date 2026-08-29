import * as React from "react"

const Checkbox = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input
    type="checkbox"
    ref={ref}
    className={`h-4 w-4 rounded border border-gray-300 bg-white text-primary focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className || ''}`}
    {...props}
  />
))
Checkbox.displayName = "Checkbox"

export { Checkbox }
