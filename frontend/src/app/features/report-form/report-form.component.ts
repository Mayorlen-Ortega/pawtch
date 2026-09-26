import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { LocationOption, ReportType } from '../../core/models';

@Component({
  selector: 'app-report-form',
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './report-form.component.html',
  styleUrl: './report-form.component.scss',
})
export class ReportFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(ApiService);
  readonly form = this.fb.nonNullable.group({
    species: ['', Validators.required], color: ['', Validators.required], markings: ['', Validators.required],
    name: [''], sex: [''], size: [''], description: [''], locationId: ['', Validators.required], date: ['', Validators.required],
  });
  locations: LocationOption[] = [];
  type: ReportType = 'lost';
  photo?: File;
  photoName = '';
  photoError = '';
  submitError = '';
  submitting = false;

  ngOnInit(): void {
    this.type = this.route.snapshot.paramMap.get('type') === 'found' ? 'found' : 'lost';
    this.api.getLocations().subscribe({ next: (locations) => this.locations = locations });
  }

  get isLost(): boolean { return this.type === 'lost'; }
  get dateLabel(): string { return this.isLost ? 'Date it was lost' : 'Date it was found'; }
  get locationLabel(): string { return this.isLost ? 'Where was your pet lost?' : 'Where was the pet found?'; }

  onPhoto(event: Event): void {
    const input = event.target as HTMLInputElement;
    const selected = input.files?.[0];
    this.photoError = '';
    if (!selected) return;
    if (!selected.type.startsWith('image/')) {
      this.photo = undefined; this.photoName = ''; this.photoError = 'That file could not be used as a photo. Please try an image file.'; return;
    }
    this.photo = selected; this.photoName = selected.name;
  }

  submit(): void {
    this.submitError = '';
    this.form.markAllAsTouched();
    if (!this.photo) this.photoError = 'Please add the clearest photo you have.';
    if (this.form.invalid || !this.photo) return;
    this.submitting = true;
    const payload = { type: this.type, ...this.form.getRawValue() };
    this.api.createReport(payload, this.photo).subscribe({
      next: (report) => this.router.navigate(['/reports', report.id], { queryParams: { created: '1' } }),
      error: (error: HttpErrorResponse) => {
        this.submitting = false;
        this.submitError = error.status === 503
          ? 'We could not use that photo for matching locally. Please try another image; your entries are still here.'
          : 'We could not save this report. Please try again; your entries are still here.';
      },
    });
  }
}
