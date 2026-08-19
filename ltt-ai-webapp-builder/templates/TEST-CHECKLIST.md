# TEST CHECKLIST

## Build

- [ ] npm run build succeeds
- [ ] lint check succeeds when configured

## Main Workflow

- [ ] page loads
- [ ] data loads
- [ ] valid action succeeds
- [ ] new data appears correctly
- [ ] refresh preserves persistent data

## Negative Tests

- [ ] missing required field rejected
- [ ] invalid value rejected
- [ ] duplicate action handled
- [ ] invalid ID handled
- [ ] unauthorized action blocked when applicable
- [ ] server failure produces useful error

## Deployment

- [ ] live URL opens
- [ ] deployed API works
- [ ] deployed database connection works
- [ ] environment variables are configured
- [ ] mobile view works
- [ ] Arabic text renders correctly
- [ ] browser console has no critical errors

## Security

- [ ] synthetic data only
- [ ] no real credentials
- [ ] .env.local absent from Git
- [ ] server secrets remain server-side
- [ ] database permissions reviewed
