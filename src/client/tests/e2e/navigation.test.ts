import { expect, test } from '@playwright/test'

test('Navigates to the correct page when a NavBar item is clicked', async ({ page }) => {
  await page.goto('http://localhost:5173/')

  await page.click('text=Graph')
  await page.waitForURL('http://localhost:5173/graph')
  expect(page.url()).toBe('http://localhost:5173/graph')

  await page.click('text=iso15926vis')
  await page.waitForURL('http://localhost:5173/')
  expect(page.url()).toBe('http://localhost:5173/')

  await page.goto('https://docs.iso15926vis.org/')
  expect(page.url()).toBe('https://docs.iso15926vis.org/')

  // No testing nav back on docs pages - just here so you know there's another home nav for now
  // await page.click('text=Home')
  // await page.waitForURL('http://localhost:5173/')
  // expect(page).toHaveURL('http://localhost:5173/')
})
