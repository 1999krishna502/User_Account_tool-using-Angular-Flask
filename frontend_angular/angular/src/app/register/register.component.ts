import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UserService } from '../user.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  constructor(private router: Router, private userService: UserService) {}

  onSubmit(form: any) {
    console.log('Form:', form); // Debug log
    console.log('Form value:', form.value); // Debug log

    if (form.valid) {
      // Ensure all fields are included
      const userDetails = {
        username: form.value.username,
        email: form.value.email,
        address: form.value.address,
        phone: form.value.phone,
        password:form.value.password
      };

      console.log('Submitting user details:', userDetails); // Debug log

      // Store user details in the service
      this.userService.setUser(userDetails);

      // Navigate to the dashboard
      this.router.navigate(['/login']);
    } else {
      console.log('Form invalid');
    }
  }
}
