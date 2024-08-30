import { expect, test } from '@playwright/test'

test('Navigates to the correct page when a NavBar item is clicked', async ({ page }) => {
  await page.goto('http://localhost:5173/')

  const docButton = await page.getByText('Documentation')
  await docButton.click()
  await expect(page).toHaveURL('http://localhost:5173/documentation')

  const homeButton = await page.getByText('Home')
  await homeButton.click()
  await expect(page).toHaveURL('http://localhost:5173/')

  const graphButton = await page.getByText('Graph')
  await graphButton.click()
  await expect(page).toHaveURL('http://localhost:5173/graph')

  const titleButton = await page.getByText('iso15926vis')
  await titleButton.click()
  await expect(page).toHaveURL('http://localhost:5173/')
})
