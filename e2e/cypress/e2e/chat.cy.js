describe('Chat functionality', () => {
  it('should allow a user to send a message and receive a bot response', () => {
    cy.visit('/');
    
    const message = 'Hello, AI!';
    cy.get('.input-area input').type(message);
    cy.get('.input-area button').click();

    # Check if the user's message appears
    cy.contains('.message.user', message);

    # Wait for the bot to respond (this might need to be more robust)
    cy.get('.message.bot', { timeout: 10000 }).should('be.visible');
  });
});
