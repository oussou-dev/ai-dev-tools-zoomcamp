import { test, expect } from '@playwright/test';

test('should execute python code and display output', async ({ page }) => {
    // Navigate to a room
    await page.goto('/room/test-room-e2e');

    // Check if the room loaded
    await expect(page.locator('h2')).toContainText('Interview Room: test-room-e2e');

    // The editor should be visible
    await expect(page.locator('.cm-editor')).toBeVisible();

    // Select Python language (default)
    await expect(page.locator('select.language-select')).toHaveValue('python');

    // Click Run Code button
    // Note: We are using the default code "// Start coding here..." which is not valid python for execution 
    // but our backend MVP executes whatever is there. 
    // Let's type some valid python code first.
    // Interacting with Monaco is hard, so we'll just use the default text for now 
    // OR we can try to click and type.
    // For simplicity, let's just run the default code. 
    // Wait, "// Start coding here..." is a comment in JS/C++, but in Python it's a comment too? 
    // Yes, # is comment in Python. // is not.
    // So executing "// Start coding here..." in Python will raise SyntaxError.
    // That's fine, we just want to see *some* output from the backend.

    await page.click('.run-btn');

    // Check for "Running python code..." message
    await expect(page.locator('.output-panel')).toContainText('Running python code...');

    // Wait for the response from the backend
    // The backend returns "Error: ..." or the output.
    // The default code is now valid Python, so we expect "Hello, World!"
    await expect(page.locator('.output-content pre')).toContainText('Hello, World!');
});
