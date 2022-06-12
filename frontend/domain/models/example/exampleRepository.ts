import { ExampleItem, ExampleItemList, ExampleAssignment } from '~/domain/models/example/example'

export type SearchOption = {[key: string]: string | (string | null)[]}

export interface ExampleRepository {
  list(projectId: string, { limit, offset, q, isChecked, isConfirmed, isApproved }: SearchOption): Promise<ExampleItemList>

  create(projectId: string, item: ExampleItem): Promise<ExampleItem>

  update(projectId: string, item: ExampleItem): Promise<ExampleItem>

  bulkDelete(projectId: string, ids: number[]): Promise<void>

  deleteAll(projectId: string): Promise<void>

  findById(projectId: string, exampleId: number): Promise<ExampleItem>

  confirm(projectId: string, exampleId: number): Promise<void>

  approval(projectId: string, exampleId: number): Promise<void>

  getAssignment(projectId: number, exampleId: number): Promise<any>
}
