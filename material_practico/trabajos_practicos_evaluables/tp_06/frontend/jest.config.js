module.exports = {
    preset: 'jest-preset-angular',
    setupFilesAfterEnv: ['<rootDir>/setup-jest.ts'],
    testEnvironment: 'jsdom',
    transform: {
        '^.+\\.(ts|mjs|html|js)$': [
            'jest-preset-angular',
            {
                tsconfig: '<rootDir>/tsconfig.spec.json',
                stringifyContentPathRegex: '\\.html$',
            },
        ],
    },
    moduleFileExtensions: ['ts', 'html', 'js', 'json'],
    moduleDirectories: ['node_modules', 'src'],
    testMatch: ['**/+(*.)+(spec).+(ts|js)?(x)'],
    collectCoverage: true,
    coverageDirectory: 'coverage',
    coverageReporters: ['html', 'text-summary'],
};
