import { assert, describe, test } from 'vitest';
import { isFieldSuitable, isFileTypeSupported } from '../src/utils/functions';

describe('isFieldSuitable', () => {
  test('field is not suitable', () => {
    assert.equal(isFieldSuitable(''), false);
  });

  test('field is not suitable', () => {
    assert.equal(isFieldSuitable('A'.repeat(30)), false);
  });

  test('field is suitable', () => {
    assert.equal(isFieldSuitable('Hello'), true);
  });
});

describe('isFileTypeSupported', () => {
  test('file type is supported', () => {
    assert.equal(isFileTypeSupported('test.pdf'), true);
  });

  test('file type is not supported', () => {
    assert.equal(isFileTypeSupported('test.doc'), false);
  });

  test('file type is supported', () => {
    assert.equal(isFileTypeSupported('test.txt'), true);
  });

  test('file type is not supported', () => {
    assert.equal(isFileTypeSupported('fdsafasd'), false);
  });
});
