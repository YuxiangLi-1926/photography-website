import importedPhotos from './importedPhotos.json';
import type { Photo } from './galleryTypes';
// Generated from the read-only Adobe inventory by scripts/import-adobe.py.
export const galleryManifest = importedPhotos as Photo[];
