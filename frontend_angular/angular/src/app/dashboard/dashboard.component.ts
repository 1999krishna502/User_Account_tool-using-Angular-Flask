import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { UserService } from '../user.service'; // Adjust path as needed

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  username: string | null = '';
  email: string | null = '';
  address: string | null = '';
  phone: string | null = '';
  router: any;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    const userDetails = this.userService.getUser();
    console.log('User details in dashboard:', userDetails); // Debug log

    if (userDetails) {
      this.username = userDetails.username;
      this.email = userDetails.email;
      this.address = userDetails.address;
      this.phone = userDetails.phone;
    } else {
      this.username = 'Guest';
      this.email = 'Not provided';
      this.address = 'Not provided';
      this.phone = 'Not provided';
    }
  }
  onEdit() {
    // Navigate to the edit page or open an edit dialog
    this.router.navigate(['/edit']);
  }

  onDelete() {
    // Confirm and delete the user
    if (confirm('Are you sure you want to delete your account?')) {
      this.userService.clearUser();
      this.router.navigate(['/login']);
    }
  }
}


