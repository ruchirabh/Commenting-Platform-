import { AbstractControl } from "@angular/forms";

export function strongPasswordValidator(control: AbstractControl) {
  const value = control.value || '';
  const strongPasswordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&^()_+=-])[A-Za-z\d@$!%*?#&^()_+=-]{8,}$/;

  return strongPasswordRegex.test(value)
    ? null
    : { weakPassword: true };
}
