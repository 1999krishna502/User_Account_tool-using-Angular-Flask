import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UserService } from '../user.service';

@Component({
  selector: 'app-edit-user',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './edit-user.component.html',
  styleUrls: ['./edit-user.component.css']
})
export class EditUserComponent implements OnInit {
  username: string | null = '';
  email: string | null = '';
  address: string | null = '';
  phone: string | null = '';

  constructor(private userService: UserService, private router: Router) {}

  ngOnInit(): void {
    const userDetails = this.userService.getUser();
    if (userDetails) {
      this.username = userDetails.username;
      this.email = userDetails.email;
      this.address = userDetails.address;
      this.phone = userDetails.phone;
    } else {
      this.router.navigate(['/login']);
    }
  }

  onSubmit(form: any) {
    if (form.valid) {
      const updatedUser = {
        username: form.value.username,
        email: form.value.email,
        address: form.value.address,
        phone: form.value.phone,
        password:form.value.password
      };

      // Update user details in the service
      this.userService.setUser(updatedUser);

      // Navigate back to the dashboard
      this.router.navigate(['/dashboard']);
    } else {
      console.log('Form invalid');
    }
  }
}
