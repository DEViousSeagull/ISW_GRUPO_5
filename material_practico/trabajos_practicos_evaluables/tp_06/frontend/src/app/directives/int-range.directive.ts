import { Directive, HostListener, ElementRef, Input } from '@angular/core';

@Directive({
    selector: '[intRange]'
})
export class IntRangeDirective {
    @Input() rangeMin = 1;
    @Input() rangeMax: number | undefined;

    private readonly controlKeys = new Set([
        'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
        'ArrowLeft', 'ArrowRight', 'Home', 'End'
    ]);

    constructor(private el: ElementRef<HTMLInputElement>) { }

    @HostListener('keydown', ['$event'])
    onKeyDown(e: KeyboardEvent) {
        const key = e.key;
        const input = this.el.nativeElement;

        // Allow control keys and shortcuts
        if (this.controlKeys.has(key) || e.ctrlKey || e.metaKey) return;

        // Only allow digits
        if (!/^\d$/.test(key)) {
            e.preventDefault();
            return;
        }

        // Predict the next value (accounting for replacement)
        const selStart = input.selectionStart ?? input.value.length;
        const selEnd = input.selectionEnd ?? input.value.length;
        let next: string;

        if (selStart === 0 && selEnd === input.value.length) {
            next = key; // replace all
        } else {
            next = input.value.slice(0, selStart) + key + input.value.slice(selEnd);
        }

        const numeric = next.replace(/\D+/g, '');
        if (numeric) {
            const num = parseInt(numeric, 10);
            // Only block if definitely above max
            if (this.rangeMax && num > this.rangeMax) {
                e.preventDefault();
            }
        }
    }


    @HostListener('paste', ['$event'])
    onPaste(e: ClipboardEvent) {
        e.preventDefault();
        const data = e.clipboardData?.getData('text') ?? '';
        const numeric = data.replace(/\D+/g, '');
        if (numeric === '') return;

        let num = parseInt(numeric, 10);

        num = Math.max(this.rangeMin, num);

        if (this.rangeMax) {
            num = Math.min(this.rangeMax, num);
        }

        this.setValue(num.toString());
    }

    @HostListener('input')
    onInput() {
        // Sanitize (e.g., from IME/auto-fill) and clamp
        const input = this.el.nativeElement;
        const cleaned = input.value.replace(/\D+/g, '');
        if (cleaned === '') {
            input.value = '';
            return;
        }
        let num = parseInt(cleaned, 10);
        num = Math.max(this.rangeMin, num);

        if (this.rangeMax) {
            num = Math.min(this.rangeMax, num);
        }
        
        if (input.value !== String(num)) {
            this.setValue(String(num));
        }
    }

    private setValue(v: string) {
        const input = this.el.nativeElement;
        input.value = v;
        // Fire native input event so Angular updates FormControl
        input.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
