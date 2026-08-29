import * as React from "react"

interface RadioGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: string;
  onValueChange?: (value: string) => void;
  name?: string;
}

const RadioGroup = React.forwardRef<HTMLDivElement, RadioGroupProps>(
  ({ className, value, onValueChange, name, children, ...props }, ref) => (
    <div ref={ref} className={`space-y-2 ${className || ''}`} {...props}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child) && child.type === RadioGroupItem) {
          return React.cloneElement(child, {
            name,
            checked: child.props.value === value,
            onChange: (e: React.ChangeEvent<HTMLInputElement>) => {
              if (onValueChange) {
                onValueChange(e.target.value);
              }
            },
          } as any);
        }
        return child;
      })}
    </div>
  )
)
RadioGroup.displayName = "RadioGroup"

const RadioGroupItem = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement> & { value: string }
>(({ className, ...props }, ref) => (
  <input
    type="radio"
    ref={ref}
    className={`h-4 w-4 border border-gray-300 text-primary focus:ring-2 focus:ring-primary focus:ring-offset-2 ${className || ''}`}
    {...props}
  />
))
RadioGroupItem.displayName = "RadioGroupItem"

export { RadioGroup, RadioGroupItem }
