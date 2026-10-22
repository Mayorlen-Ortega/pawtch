import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { Match, Report } from '../../core/models';

@Component({ selector: 'app-report-detail', imports: [CommonModule, RouterLink], templateUrl: './report-detail.component.html', styleUrl: './report-detail.component.scss' })
export class ReportDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(ApiService);
  readonly report = signal<Report | undefined>(undefined);
  readonly matches = signal<Match[]>([]);
  readonly created = signal(false);
  readonly loading = signal(true);
  readonly error = signal('');
  readonly actionLoading = signal(false);
  readonly actionError = signal('');
  ngOnInit(): void { const id = this.route.snapshot.paramMap.get('id') ?? ''; this.created.set(this.route.snapshot.queryParamMap.get('created') === '1'); this.api.getReport(id).subscribe({ next: (report) => { this.report.set(report); this.loading.set(false); }, error: () => { this.error.set('We could not find that report.'); this.loading.set(false); } }); this.api.getMatches(id).subscribe({ next: (matches) => this.matches.set(matches) }); }
  imageUrl(filename: string): string { return this.api.imageUrl(filename); }

  resolveReport(): void {
    const report = this.report();
    if (!report || report.status === 'resolved' || this.actionLoading()) return;
    if (!window.confirm('Mark this report as resolved? It will no longer appear in possible matches.')) return;

    this.actionError.set('');
    this.actionLoading.set(true);
    this.api.resolveReport(report.id).subscribe({
      next: (updatedReport) => {
        this.report.set(updatedReport);
        this.matches.set([]);
        this.actionLoading.set(false);
      },
      error: () => {
        this.actionError.set('We could not update this report. Please try again.');
        this.actionLoading.set(false);
      },
    });
  }

  deleteReport(): void {
    const report = this.report();
    if (!report || this.actionLoading()) return;
    if (!window.confirm('Permanently delete this report, its photo, and related matches?')) return;

    this.actionError.set('');
    this.actionLoading.set(true);
    this.api.deleteReport(report.id).subscribe({
      next: () => void this.router.navigateByUrl('/'),
      error: () => {
        this.actionError.set('We could not delete this report. Please try again.');
        this.actionLoading.set(false);
      },
    });
  }
}
