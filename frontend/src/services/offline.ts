import { Workbox } from 'workbox-window';

class OfflineService {
  private wb: Workbox | null = null;
  private isOnline = navigator.onLine;

  constructor() {
    this.init();
    this.setupOnlineOfflineListeners();
  }

  private init() {
    if ('serviceWorker' in navigator) {
      this.wb = new Workbox('/sw.js');

      this.wb.addEventListener('installed', (event) => {
        if (event.isUpdate) {
          console.log('New service worker installed. Refresh to update.');
          // Optionally show update notification to user
          if (confirm('New version available! Reload to update?')) {
            window.location.reload();
          }
        }
      });

      this.wb.register().catch((error) => {
        console.error('Service Worker registration failed:', error);
      });
    }
  }

  private setupOnlineOfflineListeners() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      console.log('Application is online');
      // Sync data when coming back online
      this.syncOfflineData();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      console.log('Application is offline');
    });
  }

  private async syncOfflineData() {
    // Implement offline data synchronization logic here
    console.log('Syncing offline data...');
  }

  public getOnlineStatus(): boolean {
    return this.isOnline;
  }

  public async update() {
    if (this.wb) {
      await this.wb.update();
    }
  }
}

export const offlineService = new OfflineService();
