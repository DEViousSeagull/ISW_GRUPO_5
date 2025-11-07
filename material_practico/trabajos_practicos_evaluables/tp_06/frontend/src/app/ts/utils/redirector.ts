import { Router } from '@angular/router';

/**
 * Opens a new browser tab/window safely (to avoid popup blockers),
 * and later redirects it to the desired route.
 *
 * @param router Angular Router instance
 * @param route  Target route path (e.g. '/mail')
 * @returns reference to the opened window
 */
export function openWindowAndRedirect(router: Router, route: string): Window | null {
    // Open synchronously (allowed by browsers during user click)
    const popup = window.open('about:blank', '_blank');
    if (!popup) {
        console.warn('Popup blocked or failed to open.');
        return null;
    }

    try {
        const targetUrl = router.serializeUrl(router.createUrlTree([route]));
        popup.location.href = targetUrl;
        popup.focus?.();
    } catch (err) {
        console.error('Could not redirect popup:', err);
        window.open(route, '_blank');
    }

    return popup;
}
