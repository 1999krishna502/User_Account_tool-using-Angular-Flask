import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UserService } from '../user.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  errorMessage: string | null = null;

  constructor(private router: Router, private userService: UserService) {}

  onSubmit(form: any) {
    console.log('Form:', form); // Debug log
    console.log('Form value:', form.value); // Debug log

    if (form.valid) {
      const { username, password } = form.value;

      // Validate user credentials
      if (this.userService.validateUser(username, password)) {
        // Navigate to the dashboard if login is successful
        this.router.navigate(['/dashboard']);
      } else {
        // Handle login failure
        this.errorMessage = 'Incorrect username or password';
      }
    } else {
      console.log('Form invalid');
    }
  }
}


