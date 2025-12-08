import { test, expect } from '@playwright/test';

test.describe('Real-time Collaboration', () => {
    test('should sync code changes between two users in the same room', async ({ browser }) => {
        // Create two browser contexts (simulating two users)
        const context1 = await browser.newContext();
        const context2 = await browser.newContext();

        const page1 = await context1.newPage();
        const page2 = await context2.newPage();

        // Both users navigate to the same room
        const roomUrl = 'http://localhost:5173/room/test-collaboration-room';
        await page1.goto(roomUrl);
        await page2.goto(roomUrl);

        // Wait for both editors to be visible
        await page1.waitForSelector('.cm-editor', { timeout: 10000 });
        await page2.waitForSelector('.cm-editor', { timeout: 10000 });

        // Wait a bit for WebSocket connections to establish
        await page1.waitForTimeout(1000);

        // User 1 types some code
        const editor1 = page1.locator('.cm-content');
        await editor1.click();
        await editor1.press('Control+A'); // Select all
        await editor1.type('print("Hello from User 1")');

        // Wait for debounce and network propagation
        await page1.waitForTimeout(500);

        // Check that User 2 sees the same code
        const editor2Content = await page2.locator('.cm-content').textContent();
        expect(editor2Content).toContain('Hello from User 1');

        // User 2 types some code
        const editor2 = page2.locator('.cm-content');
        await editor2.click();
        await editor2.press('Control+A'); // Select all
        await editor2.type('print("Hello from User 2")');

        // Wait for debounce and network propagation
        await page2.waitForTimeout(500);

        // Check that User 1 sees the updated code
        const editor1Content = await page1.locator('.cm-content').textContent();
        expect(editor1Content).toContain('Hello from User 2');

        // Clean up
        await context1.close();
        await context2.close();
    });

    test('should handle language changes across users', async ({ browser }) => {
        const context1 = await browser.newContext();
        const context2 = await browser.newContext();

        const page1 = await context1.newPage();
        const page2 = await context2.newPage();

        const roomUrl = 'http://localhost:5173/room/test-language-sync-room';
        await page1.goto(roomUrl);
        await page2.goto(roomUrl);

        await page1.waitForSelector('.cm-editor', { timeout: 10000 });
        await page2.waitForSelector('.cm-editor', { timeout: 10000 });

        await page1.waitForTimeout(1000);

        // User 1 changes language to JavaScript
        await page1.selectOption('select', 'javascript');

        // Wait for propagation
        await page1.waitForTimeout(500);

        // Check that User 2 sees JavaScript code snippet
        const editor2Content = await page2.locator('.cm-content').textContent();
        expect(editor2Content).toContain('console.log');

        await context1.close();
        await context2.close();
    });
});
