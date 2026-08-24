import { mediaConfig } from '../config/media';
import { galleryManifest } from '../data/galleryManifest';
import type { GalleryCategory, Photo } from '../data/galleryTypes';

export const photos = sortPhotosByOrder(galleryManifest);

export function getImageUrl(key: string): string {
  const baseUrl = mediaConfig.r2BaseUrl.replace(/\/$/, '');
  const objectKey = key.replace(/^\//, '');

  return `${baseUrl}/${objectKey}`;
}

export function sortPhotosByOrder(photoList: readonly Photo[]): Photo[] {
  return [...photoList].sort((a, b) => a.order - b.order);
}

export function getPhotosByCategory(category: GalleryCategory): Photo[] {
  return sortPhotosByOrder(
    galleryManifest.filter((photo) => photo.category === category),
  );
}

export function getFeaturedPhotos(): Photo[] {
  return sortPhotosByOrder(galleryManifest.filter((photo) => photo.featured));
}
